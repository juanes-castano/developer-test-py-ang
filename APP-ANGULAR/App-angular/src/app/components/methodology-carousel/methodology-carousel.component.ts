import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-methodology-carousel',
  standalone: true,
  templateUrl: './methodology-carousel.component.html',
})
export class MethodologyCarouselComponent {
  currentStep = signal(1);
  totalSteps = 4;

  nextStep() {
    if (this.currentStep() < this.totalSteps) {
      this.currentStep.update(step => step + 1);
    }
  }

  prevStep() {
    if (this.currentStep() > 1) {
      this.currentStep.update(step => step - 1);
    }
  }
}