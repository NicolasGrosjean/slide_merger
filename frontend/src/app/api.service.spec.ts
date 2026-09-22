import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ApiService } from './api.service';

describe('ApiService', () => {
  let service: ApiService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ApiService, provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(ApiService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads filenames with the configured query parameters', () => {
    service.getFilenames('chants', 'Kyrie').subscribe();

    const request = http.expectOne('/files/filenames?sub_directory=chants&name_filter=Kyrie');
    expect(request.request.method).toBe('GET');
    request.flush(['Kyrie.pptx']);
  });

  it('creates the merge request with the selected slides', () => {
    service.mergeSlides(['header/Vert.pptx', 'chants/Entrée.pptx'], 'service.pptx').subscribe();

    const request = http.expectOne('/slide_merger/merge');
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual({
      input_slides: ['header/Vert.pptx', 'chants/Entrée.pptx'],
      output_file_name: 'service.pptx',
    });
    request.flush(null);
  });
});
