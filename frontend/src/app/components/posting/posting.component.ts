import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { response } from 'express';
import { ApiService } from 'src/app/services/api.service';
@Component({
  selector: 'app-posting',
  templateUrl: './posting.component.html',
  styleUrls: ['./posting.component.css']
})
export class PostingComponent {
  data:any;
  file:any;
  post:any=FormGroup;
  constructor(
    private router:Router,
    private apiService:ApiService,
    private formBuilder:FormBuilder,
    private http:HttpClient
  ){}

  ngOnInit(){
    this.post = this.formBuilder.group({
      texts:['']
    });
  }

  onFileSelected(event:any) {

    this.file = event.target.files[0]
  }  
  addPost(event:any){
    if (this.file) {
      const formData = new FormData();
      const username=localStorage.getItem('username');
      console.log(username);
      if(username){
        formData.append("username",username);
      }
      formData.append("thumbnail", this.file);

      const upload$ = this.apiService.addImage(formData);
      upload$.subscribe((response)=>{
        const image_name=JSON.parse(JSON.stringify(response));
        this.data={
          username:username,
          image_name:image_name,
          texts:this.post.texts
        }
      });

    }
    this.apiService.addPost(this.data).subscribe((response)=>{
      
    });
  }
}
