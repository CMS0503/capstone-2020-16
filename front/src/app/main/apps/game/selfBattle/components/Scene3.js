import Phaser from 'phaser'

class Scene3 extends Phaser.Scene {
    constructor() {
      super("bootGame");
    }
  
    preload(){
      this.load.image("background", "assets/images/webGL/board.jpg");
      this.load.image("spinner", "assets/images/webGL/spinner.png");
      this.load.image("pawn_1", "assets/images/webGL/pawn_1.png");
      this.load.image("pawn_2", "assets/images/webGL/pawn_2.png");
      this.load.image("look_1", "assets/images/webGL/look_1.png");
      this.load.image("look_2", "assets/images/webGL/look_2.png");
      this.load.image("king_1", "assets/images/webGL/king_1.png");
      this.load.image("king_2", "assets/images/webGL/king_2.png");
      this.load.image("me", "assets/images/webGL/user.png");
      this.load.image("you", "assets/images/webGL/user2.png");
      this.load.plugin('rexsliderplugin', 'https://raw.githubusercontent.com/rexrainbow/phaser3-rex-notes/master/dist/rexsliderplugin.min.js', true); // slider bar
      this.load.image('dot', 'https://raw.githubusercontent.com/rexrainbow/phaser3-rex-notes/master/assets/images/white-dot.png'); // slider dot
    }
  
    create() {
      this.add.text(20, 20, "Loading game...");
      this.scene.start("playGame");
    }

  }

  export default Scene3;