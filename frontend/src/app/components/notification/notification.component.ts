import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';


@Component({
  selector: 'app-notification',
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.css']
})
export class NotificationComponent {
  notifications:any=[];
  constructor(private apiService:ApiService){}
  ngOnInit(){
    this.apiService.allNotifications(localStorage.getItem('username')).subscribe((data:any)=>{
      this.notifications=data;
      console.log(JSON.stringify(this.notifications));
    });
  }
}
