import { Routes } from '@angular/router';
import { CalculationPageComponent } from './pages/calculation-page/calculation-page.component';
import { HistoryPageComponent } from './pages/history-page/history-page.component';

export const routes: Routes = [
  { path: 'calculate', component: CalculationPageComponent },
  { path: 'history', component: HistoryPageComponent },
  { path: '', redirectTo: '/calculate', pathMatch: 'full' },
  { path: '**', redirectTo: '/calculate' }
];