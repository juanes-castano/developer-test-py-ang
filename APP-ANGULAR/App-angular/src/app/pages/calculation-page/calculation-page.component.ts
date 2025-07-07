import { Component, signal } from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

// Componentes
import { MethodologyCarouselComponent } from '../../components/methodology-carousel/methodology-carousel.component';
import { FileUploadComponent } from '../../components/file-upload/file-upload.component';
import { PointControlsComponent } from '../../components/point-controls/point-controls.component';
import { ResultsDisplayComponent } from '../../components/results-display/results-display.component';

// Servicios
import { ImageProcessingService } from '../../services/image-processing.service';
import { AreaCalculationService } from '../../services/area-calculation.service';
import { ResultsStorageService } from '../../services/results-storage.service';

// Modelos
import { CalculationResult } from '../../models/calculation-result.model';

@Component({
  selector: 'app-calculation-page',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    DecimalPipe,
    MethodologyCarouselComponent,
    FileUploadComponent,
    PointControlsComponent,
    ResultsDisplayComponent
  ],
  templateUrl: './calculation-page.component.html',
  styleUrls: ['./calculation-page.component.scss']
})
export class CalculationPageComponent {
  imageWithPoints = signal<string | null>(null);
  currentResult = signal<CalculationResult | null>(null);
  isLoading = signal(false);

  constructor(
    private imageProcessing: ImageProcessingService,
    private areaCalculation: AreaCalculationService,
    private resultsStorage: ResultsStorageService,
    private router: Router
  ) {}

  async onCalculate(pointsCount: number) {
    this.isLoading.set(true);
    
    try {
      // 1. Generar puntos aleatorios
      this.imageProcessing.generateRandomPoints(pointsCount);
      
      // 2. Calcular resultados
      const result = this.areaCalculation.calculateArea(pointsCount);
      if (!result) return;
      
      this.currentResult.set(result);
      this.resultsStorage.addResult(result);
      
      // 3. Obtener imagen con puntos
      const imageWithPoints = this.imageProcessing.getImageWithPoints();
      this.imageWithPoints.set(imageWithPoints);
      
    } catch (error) {
      console.error('Error during calculation:', error);
    } finally {
      this.isLoading.set(false);
    }
  }

  goToHistory() {
    this.router.navigate(['/history']);
  }
}