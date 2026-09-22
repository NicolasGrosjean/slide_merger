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
        description: 'Entrance',
        subdirectory: 'chants',
        name_filter: null,
        placeholder: 'placeholder/Entrance.pptx',
        file_name: null,
      },
    ]);
    http.expectOne('/files/filenames?sub_directory=chants').flush(['Entrance.pptx']);
    fixture.detectChanges();
    fixture.nativeElement.querySelector('form').dispatchEvent(new Event('submit'));

    const mergeRequest = http.expectOne('/slide_merger/merge');
    expect(mergeRequest.request.body.input_slides).toEqual(['placeholder/Entrance.pptx']);
    mergeRequest.error(new ProgressEvent('error'));
    http.verify();
  });
});
