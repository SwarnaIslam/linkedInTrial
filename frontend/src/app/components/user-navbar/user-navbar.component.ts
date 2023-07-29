import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { NgxUiLoaderService } from 'ngx-ui-loader';

@Component({
  selector: 'app-user-navbar',
  templateUrl: './user-navbar.component.html',
  styleUrls: ['./user-navbar.component.css']
})
export class UserNavbarComponent {

  constructor(private router: Router, private ngxService: NgxUiLoaderService,
    ) { }
  

  onLogOut() {
    this.ngxService.start();
    localStorage.removeItem('token');
    this.router.navigate(['/home']).then(() => { 
      window.location.reload(); 
      this.ngxService.stop();
    });
  }

}
