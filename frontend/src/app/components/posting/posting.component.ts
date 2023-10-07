import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-posting',
  templateUrl: './posting.component.html',
  styleUrls: ['./posting.component.css']
})
export class PostingComponent implements OnInit {
  data: any;
  file: any;
  post: any=FormGroup;

  constructor(
    private router: Router,
    private apiService: ApiService,
    private formBuilder: FormBuilder,
    private http: HttpClient
  ) {}

  ngOnInit() {
    this.post = this.formBuilder.group({
      texts: new FormArray([]) // Initialize as an empty FormArray
    });
  }

  onFileSelected(event: any) {
    this.file = event.target.files[0];
  }

  addPost(event: any) {
    const texts = this.post.get('texts')?.value;
    const username = localStorage.getItem('username');

    if (!this.file && texts.length === 0) {
      return;
    }

    const formData = new FormData();
    if(username)
      formData.append('username', username);

    // Join texts with '\n' separator
    formData.append('texts', texts.join('\n'));

    if (this.file) {
      formData.append('image_file', this.file);
    }
    console.log(formData)
    console.log(JSON.stringify(formData))
    this.apiService.addPost(formData).subscribe((response) => {
      console.log(response);
    });
  }
}
