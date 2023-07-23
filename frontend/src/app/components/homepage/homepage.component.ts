import { Component } from '@angular/core';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent {

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
