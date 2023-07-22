import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class SnackBarService {

  constructor(private snackBar: MatSnackBar) { }

  openSnackBar(message: string, action: string) {

    if (action === 'error') {
      this.snackBar.open(message, 'Dismiss', {
        horizontalPosition: 'center',
        verticalPosition: 'top',
        duration: 3000,
        panelClass: ['error-snackbar']
      });
    } else {
      this.snackBar.open(message, 'Dismiss', {
        horizontalPosition: 'center',
        verticalPosition: 'top',
        duration: 3000,
        panelClass: ['success-snackbar']
      });
    }

  }
}
