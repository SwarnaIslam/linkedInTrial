import { Component } from '@angular/core';
import { Router, NavigationEnd, NavigationStart } from '@angular/router';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {

  title = 'e-library';
  getLoginStatus:boolean = false;

  constructor(private router: Router, private authService: AuthService) { }

  ngOnInit(): void {

    this.getLoginStatus = this.authService.getLoginStatus();
    if(this.getLoginStatus){
      this.router.navigate(['notification']);
    }
    else{
      this.router.navigate(['signup']);
    }
  }
}
