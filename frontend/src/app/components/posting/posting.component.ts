import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
@Component({
  selector: 'app-posting',
  templateUrl: './posting.component.html',
  styleUrls: ['./posting.component.css']
})
export class PostingComponent {
  data:any;
  fileToUpload:any;
  post:any=FormGroup;
  constructor(
    private router:Router,
    private apiService:ApiService,
    private formBuilder:FormBuilder,
    private http:HttpClient
  ){}

  ngOnInit(){
    this.post = this.formBuilder.group({
      image_name:[''],
      username:[''],
      texts:['']
    });
  }

  onFileSelected(event:any) {

    const file: File = event.target.files[0]
    console.log(`onFileSelected(${file.name})`)

    if (file) {
      const formData = new FormData();
      formData.append("thumbnail", file);
      const upload$ = this.http.post("http://localhost:8000/thumbnail-upload", formData);
      upload$.subscribe();
      console.log("upload done?")
    }

  }  
}
