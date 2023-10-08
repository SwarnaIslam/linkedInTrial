import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SnackBarService } from './snack-bar.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  url = 'http://localhost:8080';
  boundary: any = Math.random().toString().substr(2);

  constructor(private http: HttpClient, private snackBarService: SnackBarService) { }

  checkServer(): any {
    return this.http.get(this.url);
  }

  login(data: any) {
    return this.http.post(this.url + '/auth/login', JSON.stringify(data), {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }

  signup(data: any) {
    return this.http.post(this.url + '/auth/signup', JSON.stringify(data), {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
  }


  allPosts() {
    const posts=this.http.get(this.url + '/post', {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
    return posts;
  }

  getPost(postId:number){
    const post = this.http.get(this.url+'/post/'+postId,{
      headers: new HttpHeaders().set('Content-Type','application/json')
    });
    return post;
  }
  addPost(data: any) {
    return this.http.post(this.url + '/post',data);
  }
  
  allNotifications(username:any){
    const notifications=this.http.get(this.url + '/notification/'+username, {
      headers: new HttpHeaders().set('Content-Type', 'application/json')
    });
    console.log(notifications);
    return notifications;
  }

}
