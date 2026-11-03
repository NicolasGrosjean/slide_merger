import { Component, OnInit, inject, signal } from '@angular/core';
import { FormArray, FormBuilder, FormControl, ReactiveFormsModule } from '@angular/forms';
import { ApiService, SlidePartConfig } from './api.service';

@Component({
  selector: 'app-root',
  imports: [ReactiveFormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  private readonly formBuilder = inject(FormBuilder);
  private readonly api = inject(ApiService);

  protected readonly slideParts = signal<SlidePartConfig[]>([]);
  protected readonly fileOptions = signal<string[][]>([]);
  protected readonly searchTerms = signal<string[]>([]);
  protected readonly activeSearchIndex = signal<number | null>(null);
  protected readonly activeOptionIndex = signal(-1);
  protected readonly configState = signal<'loading' | 'ready' | 'error'>('loading');
  protected readonly isSubmitting = signal(false);
  protected readonly statusMessage = signal('');
  protected readonly errorMessage = signal('');
  private readonly outputFileName = 'merged.pptx';

  protected readonly form = this.formBuilder.group({
    slideSelections: this.formBuilder.array<FormControl<string | null>>([]),
  });

  ngOnInit(): void {
    this.loadConfiguration();
  }

  protected get slideSelections(): FormArray<FormControl<string | null>> {
    return this.form.controls.slideSelections;
  }

  protected visiblePartNumber(settingsIndex: number): string {
    const visibleIndex = this.slideParts()
      .slice(0, settingsIndex + 1)
      .filter((part) => !part.file_name).length;
    return visibleIndex.toString().padStart(2, '0');
  }

  protected filteredFileOptions(index: number): string[] {
    const query = this.normalizeSearchText(this.searchTerms()[index] ?? '');
    return (this.fileOptions()[index] ?? []).filter((fileName) => this.normalizeSearchText(fileName).includes(query));
  }

  protected updateSearch(index: number, value: string): void {
    const terms = [...this.searchTerms()];
    terms[index] = value;
    this.searchTerms.set(terms);
    this.activeSearchIndex.set(index);
    this.activeOptionIndex.set(-1);
  }

  protected openSuggestions(index: number): void {
    this.activeSearchIndex.set(index);
    this.activeOptionIndex.set(-1);
  }

  protected closeSuggestions(index: number): void {
    if (this.activeSearchIndex() === index) {
      this.activeSearchIndex.set(null);
      this.activeOptionIndex.set(-1);
    }
  }

  protected handleSearchKeydown(event: KeyboardEvent, index: number): void {
    const optionCount = this.filteredFileOptions(index).length;
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      this.activeSearchIndex.set(index);
      this.activeOptionIndex.update((current) => Math.min(current + 1, optionCount - 1));
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      this.activeSearchIndex.set(index);
      this.activeOptionIndex.update((current) => Math.max(current - 1, optionCount > 0 ? 0 : -1));
    } else if (event.key === 'Enter') {
      event.preventDefault();
      const selectedOption = this.filteredFileOptions(index)[this.activeOptionIndex()];
      if (this.activeSearchIndex() === index && selectedOption) {
        this.selectFile(index, selectedOption);
      }
    } else if (event.key === 'Escape') {
      this.closeSuggestions(index);
    }
  }

  protected selectFile(index: number, fileName: string): void {
    this.slideSelections.at(index).setValue(fileName);
    this.slideSelections.at(index).markAsDirty();
    this.updateSearch(index, fileName);
    this.closeSuggestions(index);
  }

  protected submit(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid || this.isSubmitting()) {
      return;
    }

    this.isSubmitting.set(true);
    this.statusMessage.set('');
    this.errorMessage.set('');
    const { slideSelections } = this.form.getRawValue();
    const inputSlides = slideSelections
      .map((slide, index) => {
        const part = this.slideParts()[index];
        return this.toSlidePath(slide || part?.placeholder || null, part);
      })
      .filter((slide): slide is string => slide !== null);

    this.api.mergeSlides(inputSlides, this.outputFileName).subscribe({
      next: (file) => {
        this.isSubmitting.set(false);
        this.downloadFile(file, this.outputFileName);
        this.statusMessage.set(`${this.outputFileName} was created successfully.`);
      },
      error: () => {
        this.isSubmitting.set(false);
        this.errorMessage.set('The presentation could not be created. Check the backend and try again.');
      },
    });
  }

  private loadConfiguration(): void {
    this.api.getConfig().subscribe({
      next: (parts) => {
        this.slideParts.set(parts);
        this.searchTerms.set(parts.map(() => ''));
        this.fileOptions.set(parts.map((part) => (part.file_name ? [part.file_name] : [])));
        parts.forEach((part, index) => {
          this.slideSelections.push(this.formBuilder.control<string | null>(part.file_name ?? null));
          if (!part.file_name) {
            this.loadFiles(index, part);
          }
        });
        this.configState.set('ready');
      },
      error: () => {
        this.configState.set('error');
        this.errorMessage.set('The slide configuration could not be loaded. Check the backend and try again.');
      },
    });
  }

  private loadFiles(index: number, part: SlidePartConfig): void {
    this.api.getFilenames(part.subdirectory, part.name_filter).subscribe({
      next: (fileNames) => {
        const allOptions = [...this.fileOptions()];
        allOptions[index] = fileNames;
        this.fileOptions.set(allOptions);
      },
      error: () => this.errorMessage.set(`Files for ${part.description ?? part.subdirectory} could not be loaded.`),
    });
  }

  private toSlidePath(fileName: string | null, part: SlidePartConfig | undefined): string | null {
    if (!fileName || !part) {
      return null;
    }
    if (fileName.includes('/')) {
      return fileName;
    }
    return `${part.subdirectory}/${fileName}`;
  }

  private normalizeSearchText(value: string): string {
    return value
      .replace(/[\u2018\u2019\u02BC\u0060\u00B4]/g, "'")
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLocaleLowerCase();
  }

  private downloadFile(file: Blob, fileName: string): void {
    const downloadUrl = URL.createObjectURL(file);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = fileName;
    link.click();
    URL.revokeObjectURL(downloadUrl);
  }
}
