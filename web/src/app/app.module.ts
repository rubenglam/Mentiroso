import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './components/auth/login/login.component';
import { GameComponent } from './components/game/game.component';

import { SocketIoModule } from 'ngx-socket-io';
import { CookieService } from 'ngx-cookie-service';

const appRoutes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'game', component: GameComponent, data: { userName: 'userName' } },
];

@NgModule({
  declarations: [AppComponent, LoginComponent, GameComponent],
  imports: [
    BrowserModule,
    FormsModule,
    SocketIoModule,
    ReactiveFormsModule,
    RouterModule.forRoot(appRoutes),
  ],
  exports: [RouterModule],
  providers: [CookieService],
  bootstrap: [AppComponent],
})
export class AppModule { }
