from models import Grid, dimension, cell

glider_explosion = Grid(
    dimension(50, 50),
    {
        cell(2, 2),
        cell(3, 3),
        cell(3, 4),
        cell(2, 4),
        cell(1, 4),
        cell(18, 14),
        cell(18, 15),
        cell(17, 14),
        cell(17, 15),
        cell(16, 15),
        cell(15, 15),
    }
)
