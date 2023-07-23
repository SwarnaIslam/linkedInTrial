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
    console.log(event.target.files);
    this.file = event.target.files[0]
  }  
  addPost(event:any){
    const texts=this.post.value;
    const username=localStorage.getItem('username');
    if(!this.file && !texts.texts){
      return;
    }
    if (this.file) {
      console.log("pic uploading");
      const formData = new FormData();

      if(username){
        formData.append("username",username);
      }
      formData.append("thumbnail", this.file);

      const upload$ = this.apiService.addImage(formData);
      upload$.subscribe((response)=>{
        const image_name=JSON.parse(JSON.stringify(response));
        this.data={
          username:username,
          image_name:image_name["token"],
          texts:texts.texts?texts.texts:null
        }
        console.log(this.data);
      });

    }
    else{
      this.data={
        username:username,
        image_name:null,
        texts:texts.texts
      }
    }
    this.apiService.addPost(this.data).subscribe((response)=>{
      console.log(response);
    });
  }
}
