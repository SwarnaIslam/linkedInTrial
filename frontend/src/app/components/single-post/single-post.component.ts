import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
@Component({
  selector: 'app-single-post',
  templateUrl: './single-post.component.html',
  styleUrls: ['./single-post.component.css']
})
export class SinglePostComponent {
  post:any;
  constructor(private route:ActivatedRoute, private router:Router, private apiService:ApiService){}

  ngOnInit(){
    this.route.queryParams.subscribe(para=>{
      this.apiService.getPost(para['postId']).subscribe((res:any)=>{
        this.post=res;
      })
      
      console.log(para['postId']);
    })
  }
}
