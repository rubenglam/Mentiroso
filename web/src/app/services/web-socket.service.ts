// import { Injectable, EventEmitter, Output } from '@angular/core';

// import { Socket } from 'ngx-socket-io';
// import { environment } from 'src/environments/environment';
// import { CookieService } from 'ngx-cookie-service';

// @Injectable({
//   providedIn: "root"
// })
// export class SocketProviderConnect extends Socket {
//   outEven: EventEmitter<any> = new EventEmitter();

//   io = {
//     url: environment.serverSocket,
//     autoConnect: true
//   };

//   constructor(private cookieService: CookieService) {
//     //super();
//     //this.ioSocket.on('message', (res: any) => this.outEven.emit(res));
//   }

//   //   emitEvent = (event = 'default', payload = {}) => {
//   //     this.ioSocket.emit('default', {
//   //       cookiePayload: this.cookieService.get('user'),
//   //       event,
//   //       payload,
//   //     });
//   //   };
// }
