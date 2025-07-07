export interface CalculationResult {
  id: string;
  timestamp: number;
  imageName: string;
  pointsInSpot: number;
  totalPoints: number;
  estimatedArea: number;
  imageSize: {
    width: number;
    height: number;
  };
  coveragePercentage: number;
}