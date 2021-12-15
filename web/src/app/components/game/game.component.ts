import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap, Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
// import { SocketProviderConnect } from 'src/app/services/web-socket.service';
import { Carta } from '../../models/carta';
import { environment } from '../../../environments/environment.prod';
import { io } from 'socket.io-client';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css'],
})
export class GameComponent implements OnInit {
  userName: string = '';
  socket: any;

  constructor(private route: ActivatedRoute, private router: Router, private cookieService: CookieService) {
    this.socket = io(environment.serverSocket, { transports : ['websocket'] });
    this.socket.on("connect", () => {
      console.log(this.socket.id); // x8WIv7-mJelg7on_ALbx
    });
  }

  ngOnInit(): void {
    this.userName = this.route.snapshot.paramMap.get('userName')!;
    this.cookieService.set("userName", this.userName);
  }
}
