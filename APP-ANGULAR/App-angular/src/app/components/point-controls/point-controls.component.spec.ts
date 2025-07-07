import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PointControlsComponent } from './point-controls.component';

describe('PointControlsComponent', () => {
  let component: PointControlsComponent;
  let fixture: ComponentFixture<PointControlsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PointControlsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PointControlsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
