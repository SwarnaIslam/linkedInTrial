import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from './components/homepage/homepage.component';
import { LoginComponent } from './components/login/login.component';
import { SignupComponent } from './components/signup/signup.component';
import { PostingComponent } from './components/posting/posting.component';
import { NotificationComponent } from './components/notification/notification.component';
import { SinglePostComponent } from './components/single-post/single-post.component';

const routes: Routes = [
  {path:"home",component:HomepageComponent},
  {path:"singlePost", component:SinglePostComponent},
  {path:"login", component: LoginComponent},
  {path:"signup", component: SignupComponent},
  {path:"posting",component:PostingComponent},
  {path:"notification",component: NotificationComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
