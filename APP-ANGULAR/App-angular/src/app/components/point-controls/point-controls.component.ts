import { Component, Output, EventEmitter, input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule, DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-point-controls',
  standalone: true,
  imports: [FormsModule, CommonModule, DecimalPipe],
  templateUrl: './point-controls.component.html'
})
export class PointControlsComponent {
  @Output() calculate = new EventEmitter<number>();
  isLoading = input<boolean>(false);
  
  pointsCount = 1000;
  readonly minPoints = 100;
  readonly maxPoints = 10000;
  readonly step = 100;

  generatePoints() {
    if (!this.isLoading()) {
      this.calculate.emit(this.pointsCount);
    }
  }
}