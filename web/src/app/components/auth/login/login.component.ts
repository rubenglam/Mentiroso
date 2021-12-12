import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: 'login.component.html',
  styleUrls: ['login.component.css']
})
export class LoginComponent {
  title: string = "Login";

  loginForm = this.formBuilder.group({
    userName: ''
  });

  constructor(private router: Router, private formBuilder: FormBuilder) {
  }

  login() {
    const data = this.loginForm.value;
    console.log(data.userName);
    this.router.navigate(["game", { userName: data.userName }]);
  }
}
