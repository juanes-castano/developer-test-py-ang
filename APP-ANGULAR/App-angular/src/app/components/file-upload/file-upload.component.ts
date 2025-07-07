import { Component, output } from '@angular/core';
import { ImageProcessingService } from '../../services/image-processing.service';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  templateUrl: './file-upload.component.html',
  styles: `
    .drag-active {
      @apply border-blue-500 bg-blue-50;
    }
  `
})
export class FileUploadComponent {
  imageLoaded = output<void>();
  fileName = '';
  errorMessage = '';
  isDragging = false;

  constructor(private imageProcessing: ImageProcessingService) {}

  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    await this.processFile(file);
  }

  async onDrop(event: DragEvent) {
    event.preventDefault();
    this.isDragging = false;
    const file = event.dataTransfer?.files?.[0];
    await this.processFile(file);
  }

  private async processFile(file: File | undefined) {
    this.errorMessage = '';
    if (!file) return;
    
    if (!file.type.match('image.*')) {
      this.errorMessage = 'Por favor, sube un archivo de imagen válido.';
      return;
    }
    
    this.fileName = file.name;
    
    try {
      await this.imageProcessing.loadImage(file);
      this.imageLoaded.emit();
    } catch (err) {
      console.error('Error loading image', err);
      this.errorMessage = 'Error al cargar la imagen. Inténtalo de nuevo.';
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    this.isDragging = true;
  }

  onDragLeave() {
    this.isDragging = false;
  }
}