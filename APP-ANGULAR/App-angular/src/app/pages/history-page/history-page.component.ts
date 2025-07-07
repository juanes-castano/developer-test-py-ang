import { Component } from '@angular/core';
import { CalculationResult } from '../../models/calculation-result.model';
import { ResultsStorageService } from '../../services/results-storage.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-history-page',
  templateUrl: './history-page.component.html',
  styleUrls: ['./history-page.component.scss']
})
export class HistoryPageComponent {
  constructor(
    public resultsStorage: ResultsStorageService,
    private router: Router
  ) {}

  get results() {
    return this.resultsStorage.getHistory();
  }

  clearHistory() {
    this.resultsStorage.clearHistory();
  }

  formatDate(timestamp: number) {
    return new Date(timestamp).toLocaleString();
  }

  navigateToCalculation() {
    this.router.navigate(['/calculate']);
  }
}