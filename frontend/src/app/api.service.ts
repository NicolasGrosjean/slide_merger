import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface SlidePartConfig {
  description: string | null;
  subdirectory: string;
  name_filter: string | null;
  placeholder: string | null;
  file_name: string | null;
}

export interface MergeSlidesRequest {
  input_slides: string[];
  output_file_name: string;
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);

  getConfig(): Observable<SlidePartConfig[]> {
    return this.http.get<SlidePartConfig[]>('/slide_merger/config');
  }

  getFilenames(subDirectory: string, nameFilter: string | null): Observable<string[]> {
    let params = new HttpParams().set('sub_directory', subDirectory);
    if (nameFilter) {
      params = params.set('name_filter', nameFilter);
    }
    return this.http.get<string[]>('/files/filenames', { params });
  }

  mergeSlides(inputSlides: string[], outputFileName: string): Observable<void> {
    const request: MergeSlidesRequest = {
      input_slides: inputSlides,
      output_file_name: outputFileName,
    };
    return this.http.post<void>('/slide_merger/merge', request);
  }
}
