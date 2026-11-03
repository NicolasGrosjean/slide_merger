import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { App } from './app';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should show the loading state before configuration arrives', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Loading the slide library');
  });

  it('prefixes a fixed filename with its configured subdirectory when merging', () => {
    const fixture = TestBed.createComponent(App);
    const http = TestBed.inject(HttpTestingController);
    fixture.detectChanges();

    http.expectOne('/slide_merger/config').flush([
      {
        description: null,
        subdirectory: 'autre',
        name_filter: null,
        placeholder: null,
        file_name: '_Transition.pptx',
      },
    ]);
    fixture.detectChanges();
    fixture.nativeElement.querySelector('form').dispatchEvent(new Event('submit'));

    const mergeRequest = http.expectOne('/slide_merger/merge');
    expect(mergeRequest.request.body.input_slides).toEqual(['autre/_Transition.pptx']);
    expect(mergeRequest.request.body.output_file_name).toBe('merged.pptx');
    mergeRequest.error(new ProgressEvent('error'));
    http.verify();
  });

  it('uses the configured placeholder when no slide is selected', () => {
    const fixture = TestBed.createComponent(App);
    const http = TestBed.inject(HttpTestingController);
    fixture.detectChanges();

    http.expectOne('/slide_merger/config').flush([
      {
        description: null,
        subdirectory: 'autre',
        name_filter: null,
        placeholder: null,
        file_name: '_Transition.pptx',
      },
      {
        description: 'Entrance',
        subdirectory: 'chants',
        name_filter: null,
        placeholder: 'placeholder/Entrance.pptx',
        file_name: null,
      },
    ]);
    http.expectOne('/files/filenames?sub_directory=chants').flush(['Entrance.pptx']);
    fixture.detectChanges();
    const searchInput = fixture.nativeElement.querySelector('#slide-1') as HTMLInputElement;
    searchInput.dispatchEvent(new FocusEvent('focus'));
    fixture.detectChanges();
    const options = fixture.nativeElement.querySelectorAll('[role="option"]');
    expect(options).toHaveLength(1);
    expect(options[0].textContent).toContain('Entrance.pptx');
    fixture.nativeElement.querySelector('form').dispatchEvent(new Event('submit'));

    const mergeRequest = http.expectOne('/slide_merger/merge');
    expect(mergeRequest.request.body.input_slides).toEqual([
      'autre/_Transition.pptx',
      'placeholder/Entrance.pptx',
    ]);
    mergeRequest.error(new ProgressEvent('error'));
    http.verify();
  });

  it('filters suggestions and selects a file into the merge request', () => {
    const fixture = TestBed.createComponent(App);
    const http = TestBed.inject(HttpTestingController);
    fixture.detectChanges();

    http.expectOne('/slide_merger/config').flush([
      {
        description: 'Entrance',
        subdirectory: 'chants',
        name_filter: null,
        placeholder: 'placeholder/Entrance.pptx',
        file_name: null,
      },
    ]);
    http.expectOne('/files/filenames?sub_directory=chants').flush(['Entrance.pptx', 'Evening song.pptx']);
    fixture.detectChanges();

    const searchInput = fixture.nativeElement.querySelector('#slide-0') as HTMLInputElement;
    searchInput.value = 'even';
    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    fixture.detectChanges();

    const options = Array.from(fixture.nativeElement.querySelectorAll('[role="option"]')) as HTMLElement[];
    expect(options.map((option) => option.textContent?.trim())).toEqual(['Evening song.pptx']);
    options[0].click();
    fixture.detectChanges();
    expect(searchInput.value).toBe('Evening song.pptx');

    fixture.nativeElement.querySelector('form').dispatchEvent(new Event('submit'));
    const mergeRequest = http.expectOne('/slide_merger/merge');
    expect(mergeRequest.request.body.input_slides).toEqual(['chants/Evening song.pptx']);
    mergeRequest.error(new ProgressEvent('error'));
    http.verify();
  });

  it('matches straight apostrophes against curly apostrophes in filenames', () => {
    const fixture = TestBed.createComponent(App);
    const http = TestBed.inject(HttpTestingController);
    fixture.detectChanges();

    http.expectOne('/slide_merger/config').flush([
      {
        description: null,
        subdirectory: 'autre',
        name_filter: null,
        placeholder: null,
        file_name: '_Transition.pptx',
      },
      {
        description: 'Entrance',
        subdirectory: 'chants',
        name_filter: null,
        placeholder: 'placeholder/Entrance.pptx',
        file_name: null,
      },
    ]);
    http.expectOne('/files/filenames?sub_directory=chants').flush(["Qu’exulte tout l’univers.pptx"]);
    fixture.detectChanges();

    const searchInput = fixture.nativeElement.querySelector('#slide-1') as HTMLInputElement;
    searchInput.value = "Qu'ex";
    searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    fixture.detectChanges();

    const options = Array.from(fixture.nativeElement.querySelectorAll('[role="option"]')) as HTMLElement[];
    expect(options.map((option) => option.textContent?.trim())).toEqual(["Qu’exulte tout l’univers.pptx"]);
    http.verify();
  });

  it('keeps API files visible even when the file is configured as a placeholder', () => {
    const fixture = TestBed.createComponent(App);
    const http = TestBed.inject(HttpTestingController);
    fixture.detectChanges();

    http.expectOne('/slide_merger/config').flush([
      {
        description: 'Header',
        subdirectory: 'header',
        name_filter: null,
        placeholder: 'header/Vert.pptx',
        file_name: null,
      },
    ]);
    http.expectOne('/files/filenames?sub_directory=header').flush(['Blanc.pptx', 'Vert.pptx', 'Violet.pptx']);
    fixture.detectChanges();
    const searchInput = fixture.nativeElement.querySelector('#slide-0') as HTMLInputElement;
    searchInput.dispatchEvent(new FocusEvent('focus'));
    fixture.detectChanges();

    const options = Array.from(fixture.nativeElement.querySelectorAll('[role="option"]')) as HTMLElement[];
    expect(options.map((option) => option.textContent?.trim())).toContain('Vert.pptx');
    http.verify();
  });
});
