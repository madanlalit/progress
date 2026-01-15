class Progress < Formula
  include Language::Python::Virtualenv

  desc "Beautiful year calendar wallpapers showing yearly progress"
  homepage "https://github.com/madanlalit/progress"
  url "https://github.com/madanlalit/progress/archive/v1.0.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"  # Will be calculated after first release
  license "MIT"

  depends_on "python@3.11"

  resource "Pillow" do
    url "https://files.pythonhosted.org/packages/cd/74/ad3d526f3bf7b6d3f408b73fde271ec69dfac8b81341a318ce825f2b3812/pillow-10.4.0.tar.gz"
    sha256 "166c1cd4d24309b30d61f79f4a9114b7b2313d7450912277855ff5dfd7cd4a06"
  end

  def install
    virtualenv_install_with_resources
  end

  def caveats
    <<~EOS
      To generate your first wallpaper, run:
        progress generate

      To enable daily automatic updates:
        progress install

      For help and more options:
        progress --help
    EOS
  end

  test do
    system bin/"progress", "--version"
    system bin/"progress", "generate", "--no-set", "--mode", "week"
  end
end
