import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BorrowedDetailsComponent } from './borrowed-details/borrowed-details.component';
import { MatButtonModule } from '@angular/material/button';
import { UserNavbarComponent } from './user-navbar/user-navbar.component';



@NgModule({
  declarations: [
    BorrowedDetailsComponent,
    UserNavbarComponent
  ],
  imports: [
    CommonModule,
    MatButtonModule
  ]
})


export class UserModule { }
