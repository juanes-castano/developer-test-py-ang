import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MethodologyCarouselComponent } from './methodology-carousel.component';

describe('MethodologyCarouselComponent', () => {
  let component: MethodologyCarouselComponent;
  let fixture: ComponentFixture<MethodologyCarouselComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MethodologyCarouselComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MethodologyCarouselComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
