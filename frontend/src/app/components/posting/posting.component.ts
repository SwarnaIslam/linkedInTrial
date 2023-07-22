import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
@Component({
  selector: 'app-posting',
  templateUrl: './posting.component.html',
  styleUrls: ['./posting.component.css']
})
export class PostingComponent {
  data:any;
  fileToUpload:any;
  post:any=FormGroup;
  constructor(
    private router:Router,
    private apiService:ApiService,
    private formBuilder:FormBuilder
  ){}

  ngOnInit(){
    this.post = this.formBuilder.group({
      image_name:[''],
      username:[''],
      texts:['']
    });
  }

  onFileSelected(event: any) {
    this.fileToUpload = <File>event.target.files[0];
  }

  addBooks(event: any) {

    var bookData = this.post.value;

    // save image and send to server
    event.preventDefault();
    const formData = new FormData();

    formData.append('image', this.fileToUpload, this.fileToUpload.name);

    this.apiService.addImage(formData).subscribe(
      (response) => {

        this.data = {
          id: bookData.bookID,
          title: bookData.bookTitle,
          author: bookData.bookAuthor,
          description: bookData.description,
          shelf: bookData.bookShelf,
          total_quantity: bookData.availableCopies,
          available_quantity: bookData.availableCopies,
          imageUrl: "D:\\images\\" + this.fileToUpload.name,
          softcopyUrl: bookData.softCopyURL,
          category: this.selectedCategory,
        }

      },
      (error) => {
        console.log(error);
      }
    );

    this.apiService.addBooks(this.data).subscribe(
      (response: any) => {
        console.log("RES: ", response);
        this.ngxService.stop();
        this.responseMsg = response?.message;
        this.snackBarService.openSnackBar(this.responseMsg, '');
        this.router.navigate(['/all-books-record']);
      }, (error) => {
        console.log("Error: ", error)
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
