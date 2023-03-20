import hero from './resources/images/hero-plane.jpg';
import './App.css';

function App() {
  return (
    <div>
      <Header />
    </div>
  );
}

function Header(props) {
  return (
    <>
      <header>
        <img class="hero" src={hero}></img>
        <a href="#" class="logo" alt="">Roam!</a>
        <div class="toggle"/>
        <nav>
          <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">Profile</a></li>
            <li><a href="#">Team</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
        </nav>
      </header>
      <section>
        <h2>Section's Header lorem ipsum</h2>
        <p>
          Aenean placerat, nibh nec finibus porta, est lorem dignissim neque, in elementum ligula mauris id mi. Pellentesque at enim interdum, pulvinar ex non, maximus ligula. Vivamus condimentum euismod tellus, ut pulvinar neque placerat ac. Quisque maximus sodales malesuada. Nulla sodales feugiat risus, eu gravida sem elementum sit amet. Sed non commodo diam. Quisque vel nisl interdum, tincidunt sem et, lobortis felis. Mauris non faucibus leo, sit amet scelerisque leo. Duis tincidunt auctor ex sollicitudin finibus. Integer tincidunt auctor nisi, a vulputate elit tristique lobortis. Ut rutrum mauris nunc, eu rhoncus orci aliquet a. Fusce eu lectus nisi. Sed eu commodo tellus. Donec sit amet lobortis est. Morbi ante sem, bibendum ut accumsan blandit, ultrices nec dui. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
        </p>
        <p>
          Fusce condimentum urna tempus arcu varius, sodales imperdiet elit venenatis. Mauris eu ex quis tellus faucibus blandit. Vestibulum elementum metus sed eros bibendum fermentum. Maecenas ac felis et eros tincidunt tristique commodo sit amet dolor. Curabitur ullamcorper eros eu libero commodo, eu mattis lacus molestie. Sed egestas ullamcorper metus et semper. Morbi urna tellus, ultrices a viverra at, aliquet sit amet turpis. Sed vel nibh non ex porta dapibus. Quisque fringilla hendrerit maximus. Vivamus suscipit auctor diam, sed scelerisque risus ultricies eget. Maecenas nec est tortor. Aenean eu feugiat ex. Maecenas faucibus ex a sem ultricies semper. Sed vitae risus sollicitudin, vehicula diam quis, pharetra dolor. Sed pulvinar est at ullamcorper molestie. Aliquam lacinia ut arcu ut gravida.
        </p>
        <p>
          In vel dui in mauris volutpat placerat semper vel libero. Proin convallis ex mollis eros mattis, maximus molestie arcu pulvinar. Vivamus convallis massa consectetur condimentum tristique. Nullam suscipit vitae tellus sed finibus. Curabitur tempus urna nec volutpat fringilla. Donec augue lacus, ultricies quis ante id, viverra tincidunt turpis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam volutpat lectus varius, volutpat dolor vel, scelerisque lacus. Aliquam erat volutpat. Cras maximus tortor et lorem pulvinar, ac porta nibh bibendum. Ut mollis neque nibh, nec aliquam tortor ultrices in. Phasellus nec magna mattis erat imperdiet sagittis. Donec feugiat sagittis justo. Vestibulum interdum enim odio, eu rhoncus ligula feugiat et. Suspendisse dapibus justo sit amet mauris facilisis, quis interdum lorem euismod.
        </p>
        <p>
          Nam suscipit nisl ac aliquet mattis. Mauris ac justo hendrerit, sodales leo ac, tempus augue. Nunc sodales nunc ut mollis elementum. Nunc vel laoreet erat. In in commodo enim. In at malesuada nisi. Mauris diam metus, tempor vitae erat a, elementum tempus risus. Nunc blandit non diam quis suscipit. Aliquam eleifend, purus ut efficitur finibus, mauris nulla posuere sapien, accumsan tempor velit augue a eros.
        </p>
        <p>
          Nunc ac nisl sit amet nunc convallis fermentum in in diam. Donec sollicitudin risus leo, vitae aliquet tortor consectetur a. Ut nec lobortis tellus, et dignissim urna. Donec pellentesque volutpat urna, a aliquet leo. Donec vitae leo facilisis, varius arcu quis, laoreet eros. Morbi nunc urna, cursus vel enim venenatis, vestibulum auctor neque. Phasellus leo nisl, rutrum vitae sapien non, placerat ultrices tellus. Cras malesuada diam metus, aliquam dignissim massa suscipit eu. Duis vitae mi id neque tristique ullamcorper at quis nibh. Duis turpis massa, semper quis dolor quis, ultrices condimentum nibh. Quisque quis turpis sed metus consequat congue malesuada ac quam. Nulla tristique luctus laoreet. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;
        </p>
      </section>
    </>
  )
}

window.addEventListener("scroll", function () {
  const header = document.querySelector('header');
  if (header != null) {
    header.classList.toggle('sticky', window.scrollY > 0);
  }
})

const toggleElem = document.querySelector('.toggle');
const navigation = document.querySelector('nav');

toggleElem.addEventListener("click", function(){
  toggleElem.classList.toggle('active');
  navigation.classList.toggle('active');
})

export default App;
