import { Injectable } from '@angular/core';
import { Users } from '../models/users';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class UsersService {

  constructor(private apiService: ApiService) { }

  
  users: Users[] = [];

  userToBeViewd: Users = new Users();


  getUsers(): any {
    return this.apiService.allUsers();
  }

  getUserToBeViewed(): Users {
    return this.userToBeViewd;
  }

  setUserToBeViewed(user: Users): void {
    if (user != null) {
      this.userToBeViewd = user;
    }
  }

  deleteUser(email: string): void {
    for (let i = 0; i < this.users.length; i++) {
      if (this.users[i].email === email) {
        this.users.splice(i, 1);
      }
    }
  }

  addNewUser(user:Users):void{
    this.users.push(user);
    console.log("Approved: ",this.users);
  }
}
