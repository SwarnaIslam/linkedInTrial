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
  isUserLoggedIn: boolean = false;

  constructor(private router: Router, private authService: AuthService) { }

  ngOnInit(): void {

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationStart) {
        const navbar = window.document.getElementById("header");

      }

      if (event instanceof NavigationEnd) {
        const currentRoute = this.router.url;
        const navbar = window.document.getElementById("header");
        if (currentRoute === "/book-details" || currentRoute === "/all-books-record" || currentRoute === "/all-book-settings" || currentRoute === "/users-record" || currentRoute === "/users-settings") {
          if (navbar) {
            navbar.classList.remove("header-transparent")
          }
        }
        else {
          if (navbar) {
            navbar.classList.add("header-transparent")
          }
        }
      }
    });

    this.getLoginStatus = this.authService.getLoginStatus();

    console.log("STAT: ", this.getLoginStatus, " USR: ", this.isUserLoggedIn);
  }
}
