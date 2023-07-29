import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormGroupDirective, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgxUiLoaderService } from 'ngx-ui-loader';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { GlobalConstants } from 'src/app/shared/global-constant';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  responseMsg: any;
  registrationForm: any = FormGroup;

  constructor(
    private router: Router,
    private apiService: ApiService,
    private ngxService: NgxUiLoaderService,
    private snackBarService: SnackBarService,
    private formBuilder: FormBuilder
  ) { }

  ngOnInit(): void {
    this.registrationForm = this.formBuilder.group({
      username: [null, [Validators.required, Validators.pattern(GlobalConstants.nameRegex)]],
      email: [null, [Validators.required, Validators.pattern(GlobalConstants.emailRegex)]],
      password: [null, [Validators.required]]
    });
  }

  onSubmit() {

    this.ngxService.start();
    var formData = this.registrationForm.value;

    var data = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
    }


    this.apiService.signup(data).subscribe(
      (response: any) => {
        this.ngxService.stop();
        this.responseMsg = 'User Created Successfully';
        this.snackBarService.openSnackBar(this.responseMsg, '');
        this.router.navigate(['/login']);
      }, (error) => {
        this.ngxService.stop();
        if (error.error?.detail) {
          this.responseMsg = error.error?.detail;
        }
        else {
          this.responseMsg = GlobalConstants.genericError;
        }
        this.snackBarService.openSnackBar(this.responseMsg, GlobalConstants.error);
      });

  }


}
