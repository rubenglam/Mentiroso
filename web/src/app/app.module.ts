import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './components/auth/login/login.component';
import { GameComponent } from './components/game/game.component';

const appRoutes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'game', component: GameComponent, data: { userName: 'userName' } },
];

@NgModule({
  declarations: [AppComponent, LoginComponent, GameComponent],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    RouterModule.forRoot(appRoutes),
  ],
  exports: [RouterModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
