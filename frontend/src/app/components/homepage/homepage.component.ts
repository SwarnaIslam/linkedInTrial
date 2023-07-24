import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import axios from 'axios';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent {

  posts:any;
  constructor(private router:Router,private apiService:ApiService){
  }
  
  ngOnInit(){
    this.apiService.allPosts().subscribe((data:any)=>{
      this.posts=data;
    });
    console.log(this.posts);
  }
  getMinIOImage = async (filename: string): Promise<string> => {
    try {
      const response = await axios.get(`localhost:9000/linkedin/${filename}`, {
        responseType: "blob", // Specify that the response should be treated as a binary Blob
      });

      // Create a Blob URL from the image Blob data
      const blobUrl = URL.createObjectURL(response.data);
      return blobUrl;
    } catch (error) {
      console.error("Error fetching the image:", error);
      throw error;
    }
  };
}
// import { Component } from '@angular/core';
// import { Router } from 'express';
// import { ApiService } from 'src/app/services/api.service';

// @Component({
//   selector: 'app-homepage',
//   templateUrl: './homepage.component.html',
//   styleUrls: ['./homepage.component.css']
// })
// export class HomepageComponent {
//   posts:any;
//   constructor(
//     private apiService:ApiService,
//     private router:Router
//   ){}
//   // ngAfterViewInit() : void{
//   //   this.posts=this.apiService.allPosts();
//   // }
// }
