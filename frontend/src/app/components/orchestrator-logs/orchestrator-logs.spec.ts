import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrchestratorLogs } from './orchestrator-logs';

describe('OrchestratorLogs', () => {
  let component: OrchestratorLogs;
  let fixture: ComponentFixture<OrchestratorLogs>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrchestratorLogs]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrchestratorLogs);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
