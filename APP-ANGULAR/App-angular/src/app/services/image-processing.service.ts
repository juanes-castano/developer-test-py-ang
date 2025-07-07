import { Injectable, signal } from '@angular/core';
import { toObservable } from '@angular/core/rxjs-interop';

@Injectable({ providedIn: 'root' })
export class ImageProcessingService {
  // Cambiar a señales (signals)
  private _currentImage = signal<{image: HTMLImageElement, name: string} | null>(null);
  private _points = signal<{x: number, y: number, isInSpot: boolean}[]>([]);

  // Exponer como propiedades de solo lectura
  public currentImage = this._currentImage.asReadonly();
  public currentPoints = this._points.asReadonly();

  async loadImage(file: File): Promise<void> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          this._currentImage.set({image: img, name: file.name});
          this._points.set([]); // Resetear puntos al cargar nueva imagen
          resolve();
        };
        img.onerror = reject;
        img.src = e.target?.result as string;
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  generateRandomPoints(count: number): void {
    const imageInfo = this._currentImage();
    if (!imageInfo) return;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    canvas.width = imageInfo.image.width;
    canvas.height = imageInfo.image.height;
    ctx.drawImage(imageInfo.image, 0, 0);
    
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    
    const newPoints = Array.from({length: count}, () => {
      const x = Math.floor(Math.random() * canvas.width);
      const y = Math.floor(Math.random() * canvas.height);
      const index = (y * canvas.width + x) * 4;
      const isInSpot = data[index] === 255 && data[index + 1] === 255 && data[index + 2] === 255;
      return { x, y, isInSpot };
    });
    
    this._points.set(newPoints);
  }

  getImageWithPoints(): string | null {
    const imageInfo = this._currentImage();
    const points = this._points();
    if (!imageInfo || points.length === 0) return null;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;
    
    canvas.width = imageInfo.image.width;
    canvas.height = imageInfo.image.height;
    ctx.drawImage(imageInfo.image, 0, 0);
    
    points.forEach(point => {
      ctx.beginPath();
      ctx.arc(point.x, point.y, 3, 0, Math.PI * 2);
      ctx.fillStyle = point.isInSpot ? 'rgba(0, 255, 0, 0.8)' : 'rgba(255, 0, 0, 0.8)';
      ctx.fill();
    });
    
    return canvas.toDataURL();
  }
}