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


  allUsers() {
    return this.http.get(this.url + '/users/all_users', {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  not_approved_users() {
    return this.http.get(this.url + '/users/not_approved', {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  verify_user(data: any) {
    return this.http.post(this.url + '/users/verify_user', JSON.stringify(data), {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  allBooks() {
    return this.http.get(this.url + '/books/all_books', {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  addBooks(data: any) {
    return this.http.post(this.url + '/add-books', JSON.stringify(data), {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  updateBook(bookId: string, bookData: any) {
    return this.http.put(this.url + `/books/${bookId}`, JSON.stringify(bookData), {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  deleteBook(bookId: string) {
    return this.http.delete(this.url + `/books/${bookId}`, {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  addImage(formData: any) {
    return this.http.post(this.url + '/upload-image', formData);
  }

}
