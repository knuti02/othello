import sqlite3
"""
Create the star schema
"""

def create_db(db_name = "othello_star_schema.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # DimModel Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimModel (
            ModelID INTEGER PRIMARY KEY AUTOINCREMENT,
            Depth INTEGER,
            MobilityWeight REAL,
            StabilityWeight REAL,
            CoinWeight REAL,
            CornersWeight REAL,
            DangerZonesWeight REAL,
            EdgesWeight REAL,
            WedgesWeight REAL,
            Mobility_StandardWeight REAL,
            Mobility_DynamicMaxWeight REAL,
            Mobility_DynamicMidpoint REAL,
            Mobility_DynamicSteepness REAL,
            Stability_SafeWeight REAL,
            Stability_StableWeight REAL,
            Stability_UnstableWeight REAL,
            Stability_StandardWeight REAL,
            Stability_DynamicMaxWeight REAL,
            Stability_DynamicMidpoint REAL,
            Stability_DynamicSteepness REAL,
            Coins_StandardWeight REAL,
            Coins_DynamicMaxWeight REAL,
            Coins_DynamicMidpoint REAL,
            Coins_DynamicSteepness REAL,
            Corners_CornerWeight REAL,
            Corners_PotentialWeight REAL,
            Corners_StandardWeight REAL,
            Corners_DynamicMaxWeight REAL,
            Corners_DynamicMidpoint REAL,
            Corners_DynamicSteepness REAL,
            DangerZones_OrangePenalty REAL,
            DangerZones_RedPenalty REAL,
            DangerZones_StandardWeight REAL,
            DangerZones_DynamicMaxWeight REAL,
            DangerZones_DynamicMidpoint REAL,
            DangerZones_DynamicSteepness REAL,
            Edges_StandardWeight REAL,
            Edges_DynamicMaxWeight REAL,
            Edges_DynamicMidpoint REAL,
            Edges_DynamicSteepness REAL,
            Wedges_WedgeWeight REAL,
            Wedges_PotentialWeight REAL,
            Wedges_StandardWeight REAL,
            Wedges_DynamicMaxWeight REAL,
            Wedges_DynamicMidpoint REAL,
            Wedges_DynamicSteepness REAL
        )
    ''')
    
    
    # FactGame Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FactGame (
            GameID INTEGER PRIMARY KEY,
            BlackModelID INTEGER,
            WhiteModelID INTEGER,
            FinalScore TEXT,
            Winner TEXT,
            FOREIGN KEY (BlackModelID) REFERENCES DimModel(ModelID),
            FOREIGN KEY (WhiteModelID) REFERENCES DimModel(ModelID)
        )
    ''')
    
    # DimGameState Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimGameState (
            GameStateID INTEGER PRIMARY KEY,
            GameID INTEGER,
            CurrentPlayer TEXT,
            MoveNumber INTEGER,
            PiecesPlaced INTEGER,
            CombinedScore REAL,
            MobilityScore REAL,
            StabilityScore REAL,
            CoinsScore REAL,
            CornersScore REAL,
            DangerZonesScore REAL,
            EdgesScore REAL,
            WedgesScore REAL,
            CurrentPlayerBitboard TEXT,
            OpponentBitboard TEXT,
            FOREIGN KEY (GameID) REFERENCES FactGame(GameID)
        )
    ''')
    
    # DimMoves Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DimMoves (
            MoveID INTEGER PRIMARY KEY,
            GameID INTEGER,
            MoveNumber INTEGER,
            Player TEXT,
            Move TEXT,
            FOREIGN KEY (GameID) REFERENCES FactGame(GameID)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database and tables created successfully.")
    
if __name__ == "__main__":
    create_db()