import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SnackBarService } from './snack-bar.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  url = 'http://127.0.0.1:8000';
  boundary: any = Math.random().toString().substr(2);

  constructor(private http: HttpClient, private snackBarService: SnackBarService) { }

  checkServer(): any {
    return this.http.get(this.url);
  }

  login(data: any) {
    return this.http.post(this.url + '/login', JSON.stringify(data), {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  signup(data: any) {
    return this.http.post(this.url + '/signup', JSON.stringify(data), {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }


  allPosts() {
    return this.http.get(this.url + '/all-posts', {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }


  addPost(data: any) {
    return this.http.post(this.url + '/add-post', JSON.stringify(data), {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }


  addImage(formData: any) {
    return this.http.post(this.url + '/thumbnail-upload',formData);
  }
  

}
