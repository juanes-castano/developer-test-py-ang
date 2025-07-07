import { Injectable } from '@angular/core';
import { CalculationResult } from '../models/calculation-result.model';

@Injectable({
  providedIn: 'root' // Esta línea es crucial
})
export class ResultsStorageService {
  private history: CalculationResult[] = [];
  
  addResult(result: CalculationResult): void {
    this.history.unshift(result);
  }

  getHistory(): CalculationResult[] {
    return [...this.history]; // Devuelve una copia para evitar mutaciones directas
  }

  addToHistory(result: CalculationResult): void {
    this.history.unshift(result);
  }

  clearHistory(): void {
    this.history = [];
  }
}