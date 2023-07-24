import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent {

  posts:any=[];
  postObj:any=[];
  constructor(private router:Router,private apiService:ApiService){
  }
  
  ngOnInit(){
    this.apiService.allPosts().subscribe((data:any)=>{
      this.posts=data;
      // for(var i=0;i<this.posts.length;i++){
      //   this.imageObj.push(this.getMinIOImage(this.posts[i].image_name));
      // }
      this.postObj=JSON.stringify(this.posts);
    });

  }
  
}
