import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
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
      texts: new FormArray([this.formBuilder.control('')])
    });
  }

  onFileSelected(event:any) {
    this.file = event.target.files[0]
  }  
  addPost(event:any){
    let texts=this.post.get('texts').value;
    texts=texts.join('\n');

    const username=localStorage.getItem('username');
    if(!this.file && !texts.texts){
      return;
    }
    this.data={
      username,
      texts,
      image_file:this.file
    };
    
    this.apiService.addPost(this.data).subscribe((response)=>{
      console.log(response);
    });
  }
}
