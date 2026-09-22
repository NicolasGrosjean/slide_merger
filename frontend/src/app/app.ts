import { Component, OnInit, inject, signal } from '@angular/core';
import { FormArray, FormBuilder, FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
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
  protected readonly configState = signal<'loading' | 'ready' | 'error'>('loading');
  protected readonly isSubmitting = signal(false);
  protected readonly statusMessage = signal('');
  protected readonly errorMessage = signal('');

  protected readonly form = this.formBuilder.group({
    slideSelections: this.formBuilder.array<FormControl<string | null>>([]),
    outputFileName: this.formBuilder.nonNullable.control('merged.pptx', [
      Validators.required,
      Validators.pattern(/^[^/\\:*?"<>|]+\.pptx$/i),
    ]),
  });

  ngOnInit(): void {
    this.loadConfiguration();
  }

  protected get slideSelections(): FormArray<FormControl<string | null>> {
    return this.form.controls.slideSelections;
  }

  protected filteredFileOptions(index: number): string[] {
    const query = (this.searchTerms()[index] ?? '').trim().toLocaleLowerCase();
    return (this.fileOptions()[index] ?? []).filter((fileName) => fileName.toLocaleLowerCase().includes(query));
  }

  protected updateSearch(index: number, value: string): void {
    const terms = [...this.searchTerms()];
    terms[index] = value;
    this.searchTerms.set(terms);
  }

  protected isPlaceholder(index: number, fileName: string): boolean {
    return fileName === this.slideParts()[index]?.placeholder;
  }

  protected submit(): void {
    this.form.markAllAsTouched();
    if (this.form.invalid || this.isSubmitting()) {
      return;
    }

    this.isSubmitting.set(true);
    this.statusMessage.set('');
    this.errorMessage.set('');
    const { slideSelections, outputFileName } = this.form.getRawValue();
    const inputSlides = slideSelections
      .map((slide, index) => this.toSlidePath(slide, this.slideParts()[index]))
      .filter((slide): slide is string => slide !== null);

    this.api.mergeSlides(inputSlides, outputFileName).subscribe({
      next: () => {
        this.isSubmitting.set(false);
        this.statusMessage.set(`${outputFileName} was created successfully.`);
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
          this.slideSelections.push(
            this.formBuilder.control<string | null>(part.file_name ?? null, Validators.required),
          );
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
        const options = [...fileNames];
        if (part.placeholder && !options.includes(part.placeholder)) {
          options.push(part.placeholder);
        }
        const allOptions = [...this.fileOptions()];
        allOptions[index] = options;
        this.fileOptions.set(allOptions);
      },
      error: () => this.errorMessage.set(`Files for ${part.description ?? part.subdirectory} could not be loaded.`),
    });
  }

  private toSlidePath(fileName: string | null, part: SlidePartConfig | undefined): string | null {
    if (!fileName || !part) {
      return null;
    }
    if (part.file_name || fileName.includes('/')) {
      return fileName;
    }
    return `${part.subdirectory}/${fileName}`;
  }
}
