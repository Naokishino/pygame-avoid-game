const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

let player;
let cursors;
let enemies;
let score = 0;
let scoreText;
let speedLevel = 1;
let maxSpeedLevel = 10;

function preload() {
    // プレイヤーと敵の画像をロード
    this.load.image('player', 'assets/player.png'); // プレイヤー画像
    this.load.image('enemy', 'assets/enemy.png');  // 敵画像
}

function create() {
    // 背景色
    this.cameras.main.setBackgroundColor('#FFFFFF');

    // プレイヤーを作成
    player = this.physics.add.sprite(400, 550, 'player');
    player.setCollideWorldBounds(true); // 画面端で止める

    // 敵のグループを作成
    enemies = this.physics.add.group({
        key: 'enemy',
        repeat: 5,
        setXY: { x: 100, y: 50, stepX: 120 }
    });

    // 敵の速度を設定
    enemies.children.iterate(function (enemy) {
        enemy.setVelocity(0, Phaser.Math.Between(100, 200)); // ランダム速度
        enemy.setCollideWorldBounds(true);
        enemy.setBounce(1);
    });

    // スコア表示
    scoreText = this.add.text(10, 10, 'Score: 0', { fontSize: '32px', fill: '#000' });

    // キーボード入力を設定
    cursors = this.input.keyboard.createCursorKeys();

    // プレイヤーと敵の衝突時の処理
    this.physics.add.collider(player, enemies, gameOver, null, this);
}

function update() {
    // プレイヤーの移動処理
    if (cursors.left.isDown) {
        player.setVelocityX(-300);
    } else if (cursors.right.isDown) {
        player.setVelocityX(300);
    } else {
        player.setVelocityX(0);
    }

    if (cursors.up.isDown) {
        player.setVelocityY(-300);
    } else if (cursors.down.isDown) {
        player.setVelocityY(300);
    } else {
        player.setVelocityY(0);
    }

    // 敵の再配置とスコア更新
    enemies.children.iterate(function (enemy) {
        if (enemy.y > 600) {
            enemy.y = 0;
            enemy.x = Phaser.Math.Between(0, 800);
            score += 1;

            // スコアに応じた速度アップ
            if (score % 3 === 0 && speedLevel < maxSpeedLevel) {
                speedLevel += 1;
                enemies.children.iterate(function (enemy) {
                    enemy.setVelocityY(enemy.body.velocity.y + 20);
                });
            }
        }
    });

    // スコアを更新
    scoreText.setText('Score: ' + score);
}

function gameOver(player, enemy) {
    this.physics.pause(); // ゲームを停止
    player.setTint(0xff0000); // プレイヤーを赤くする
    scoreText.setText('Game Over!');
}
