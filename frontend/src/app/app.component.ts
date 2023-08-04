import { AfterViewInit, Component, OnInit } from "@angular/core";
import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { BehaviorSubject, Observable, throwError } from "rxjs";
import { catchError, retry } from "rxjs/operators";

@Injectable()
@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"],
})
export class AppComponent implements OnInit {
  title = "coffee_cabal";
  leastAcidicCoffee: BehaviorSubject<any> = new BehaviorSubject({});
  bestBalanceByProcessingMethod: BehaviorSubject<any> = new BehaviorSubject({});
  largestExporter: BehaviorSubject<any> = new BehaviorSubject({});

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http
      .get<any>("http://localhost:8000/least-acidic-regions")
      .subscribe((data) => {
        this.leastAcidicCoffee.next(data);
      });
    this.http
      .get<any>("http://localhost:8000/processing-method-balance")
      .subscribe((data) => {
        this.bestBalanceByProcessingMethod.next(data);
      });
    this.http
      .get<any>("http://localhost:8000/largest-exporter")
      .subscribe((data) => {
        this.largestExporter.next(data);
      });
  }
}
