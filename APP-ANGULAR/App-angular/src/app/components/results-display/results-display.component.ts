import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

interface CalculationResult {
  totalPoints: number;
  pointsInSpot: number;
  estimatedArea: number;
  imageSize: { width: number, height: number };
}

@Component({
  selector: 'app-results-display',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results-display.component.html'
})
export class ResultsDisplayComponent {
  @Input() result: CalculationResult | null = null;
  
  calculatePercentage(): number {
    if (!this.result || this.result.totalPoints === 0) return 0;
    return (this.result.pointsInSpot / this.result.totalPoints) * 100;
  }
}