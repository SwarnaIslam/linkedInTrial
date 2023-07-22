import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { NgxUiLoaderService } from 'ngx-ui-loader';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { GlobalConstants } from 'src/app/shared/global-constant';
import { ApiService } from 'src/app/services/api.service';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  responseMsg: any;

  constructor(
    private router: Router,
    private apiService: ApiService,
    private ngxService: NgxUiLoaderService,
    private snackBarService: SnackBarService,
    private authService: AuthService
  ) { }

  onSubmit() {
    this.ngxService.start();

    const data = { email: this.email, password: this.password };
    console.log(data);

    this.apiService.login(data).subscribe(
      (response: any) => {
        console.log("RES: ", response);
        this.ngxService.stop();
        this.responseMsg = response?.message;
        console.log(response.name);

        this.snackBarService.openSnackBar('Welcome ' + response.name, '');
        localStorage.setItem('token', "user");
        this.router.navigate(['/home']).then(() => { window.location.reload(); });
        

      },
      (error) => {
        console.log("Error: ", error.error.detail)
        this.ngxService.stop();
        if (error.error?.detail) {
          this.responseMsg = error.error?.detail;
        } else {
          this.responseMsg = GlobalConstants.genericError;
        }
        this.snackBarService.openSnackBar(
          this.responseMsg,
          GlobalConstants.error
        );
      },
    );
  }
}
