import { Injectable } from '@angular/core';
import { ImageProcessingService } from './image-processing.service';
import { CalculationResult } from '../models/calculation-result.model';

@Injectable({ providedIn: 'root' })
export class AreaCalculationService {
  constructor(private imageProcessing: ImageProcessingService) {}

  calculateArea(pointsCount: number): CalculationResult | null {
    // Acceder a los valores actuales de las señales
    const imageInfo = this.imageProcessing.currentImage();
    const points = this.imageProcessing.currentPoints();
    
    if (!imageInfo || !points || points.length === 0) return null;
    
    const pointsInSpot = points.filter(p => p.isInSpot).length;
    const totalArea = imageInfo.image.width * imageInfo.image.height;
    const estimatedArea = totalArea * (pointsInSpot / pointsCount);
    const coveragePercentage = (pointsInSpot / pointsCount) * 100;
    
    return {
      id: this.generateUniqueId(),
      timestamp: Date.now(),
      imageName: imageInfo.name,
      totalPoints: pointsCount,
      pointsInSpot: pointsInSpot,
      estimatedArea: estimatedArea,
      imageSize: {
        width: imageInfo.image.width,
        height: imageInfo.image.height
      },
      coveragePercentage: coveragePercentage
    };
  }

  private generateUniqueId(): string {
    return crypto.randomUUID(); // Método moderno para generar IDs únicos
  }
}