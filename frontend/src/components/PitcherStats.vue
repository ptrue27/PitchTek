<template>
    <v-card style="width: 100%; margin: 10px 10px;">
        <h3 class="ml-2">{{ player.name }}</h3>
        <v-row>
            <!--Player image-->
            <v-col cols="3">
                <v-img fluid
                    :src="player.img"
                ></v-img>
            </v-col>

            <!--Player stats-->
            <v-col cols="9" class="pr-2">
                <div>
                    <table class="stats-table">
                        <thead>
                            <tr>
                            <th>ERA</th>
                            <th>K/9</th>
                            <th>BB/9</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                            <td>{{ player.era }}</td>
                            <td>{{ player.kper9 }}</td>
                            <td>{{ player.bbper9 }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
export default {
    data(){
        return{
            player: { name: 'Justin Verlander', img: 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUWFRYWFhYYGBgZGhoVGhYcGh0YGBQaGRoZGhkaGBocIy4nHB4rHxkcJzgmKy8xNTU1HCQ+QDs0Py40NTEBDAwMEA8QHxISHjQsJCsxNDQ0PTY9NDE0NDU2PTQ0MTExNjQ0NDY2NDQ0NDQ1NT80NDQ2NDQ0NDU0NDU0NDQ0Nv/AABEIAL8BBwMBIgACEQEDEQH/xAAcAAEAAQUBAQAAAAAAAAAAAAAABQIDBAYHAQj/xAA9EAACAQIEAwYDBgQFBQEAAAABAgADEQQSITEFQVEGEyJhcYEHkaEyQlKx0fAUYnLBQ5Ky4fEjM3OzwiT/xAAZAQEAAwEBAAAAAAAAAAAAAAAAAQIDBAX/xAAnEQEBAAICAgIBBQADAQAAAAAAAQIRAyExURJhQRMiccHRMoGhBP/aAAwDAQACEQMRAD8A7NERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQE8mHxTiFPD0nrVWCpTBZm6DyHMk2AHMkThnaT4t4usWXDAYembgNo1Zh1LHRSRyUXH4jvEg7bxfjWHwq58RVSmvLMdW8lUasfIAzQeL/GPDIcuGo1MQeTH/pof6bgsfdROH1sSzuXqMzsTdmZizN6sbmdC+FfEqQxaUaaMj1TZmuHVwis5BuLroDt7mLvHXVq+OMu+5G14X4g496VSv/CU6aJeyOXz1SoBbKbCwCka2NyQBzt5wb4y4d2C4ii9G5tnU96g82AAYewabDj66vWKpikR0fKFyMSt9MvIXP8Afzmj/FzE0O+7h+7UqFqXWmDWuc2he2inQ2uOXKZzLu799NcuHckmpdbu+nXOGcVoYhc1CqlVeZRg1vI22PkZnz5FwmOqYeoKmHqujDZ18DW0JBAJuLja5BnTuy3xidcqY1M40HfoArAdXTZupK29DNdOeu2xMfCYpKqLUpsHRwGVgbhgdiJkSAiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiBy7464wrhKFIGwqVbsPxLTUm3pmZT7CcJnW/j5XvVwafhSo3+ZkH/xOShZfHwgE3Lsl2rp4CkWWjSq1nZiGIOdEsoyl/ugkMbC++s1BEubAFieQF/kBrJXDdncVUF1w7WPMgJ/qIlcsp7Xxl/E22mn8S2/iTXbC02UoqCkGKhSrl+8zZTdze17aACYXb/j+GxgpV6VLJVYstVyxZrKFyKQTbmTe3IWOhEiK3ZjGKLmgdOhRj8gSZD16RU2dCp6EFT9ZEst6q9mUmsp/H0sEzyV5RyNvX9ZQVtvLMXevgVxAtg6tEm/dVbqOi1FDW/zBz7zp84b8AsQRiMVT5NTR/dHKj/2GdylakiIgIiICIiAiIgIiICIiAiIgIiICIiAiIgIiICImPjA5RwhAcqwQnYNY5Sfe0Dgfxo4jTq48Kjhu5pLSe2yvndmW/MgMt+h03BmncI4U9dtNF5t/YSmrw6t/EGjVV1qZrOHvmBOpLX3ve9+d785uuMrDCoiUku5W4AFyOQMpnlfEbcWEv7r4iW4FwJaYsqAHmx1J9TJ1MLU8rTSKGK4iACtN7b5gAzc9LH0/4mz9l+L1mcJWTQkkkrkb5G2mv7tObLC+bXfx8mPiRKvQNgMov1/YkbxDgudSGQMOhFwfnNudFALHl+Qmhcc7UVg+WnTLAXFyDa/kBIxwu2mXJjJ21HtD2VyXZBb+Xcf7TUTdSQR6gzf8TxHHOuc4dlUbnIwB8vGPWQmP4X3yGrTHiX7Sc/OdGOVn/JwcmGOXeLYPghXC8RZb2z0HUAm1yGRrDqbKT7GfQc+PsDjHo1FqIxV0YMrcwym4/wCJ9acIxZrUKNUjKalNKhX8JdQ1vrNXKzYiICIiAiIgIiICIiAiIgIiICIiAiIgIiICIiB5LVesqKWYhVAuSTYAecuyE7TuO6CH77KPYEE/2lcr8Zathj8spj7ck7Q1KVTjL1KTBwyq2YbXWmi2F+en1ks/CFzmu652sAiXABI2BPTcyO/gQOIU2RbB6V7Hb7Vrn5fSbkSAwABe2nl0sfLyE58st3f07sOP47x+0RVbizAFO7prp4VsSvi/E24yg8hqQNRcjOTF1jcVbELYqTbPfncDY+YNrDYSQOfewXyBJHyvYfKYOLpHQnW/oPoJW3cbYcervaqtxBivlp/e35SirjcSaZFBcpUWUhVYM2m4zqRoTvzG2t5j4gnJ5e1773+Uy+FOQu1xvK47laZ8e5pF0OKY8LbEYfOhNjZVRgLC5tmYEDUXvsNpiNwhULOhGVzte5B+c296gtroN7a6e4MxMVTVkOU256HQ6S1y2y+Hx8uQ4HAU24pRR1BpviKaOuwOdgLaHYmfTNIAAAAAAWAGwA5CcBwvD0fHViwuqoHt/PcZfTQNOo9gqmlZBoqspUC9rMgN7E6HbbpN8eSbmLj5OG/G5/bcoiJq5iIiAiIgIiICIiAiIgIiICIiAiIgIiICIiBTIjtLhi9BiN08Q9t/19pMSh1BBBFwRYjqDvIym5pbDK45TKfhyelWz4waWK08im2wLtr0sAL+46zZ8FStpb2mu4qgaWOYHQpTprmPP/qPlI9V/OSmBx5WnVqPrkzG3MgC497Tlyxr0cM9232leIfZso1t9Zr1cWYLUJB0sut7GxO3r9Jg1e1pvmWwP4TqfqBY6jptMShjWrszuxshFluRmvc7H+k/l1Mn41bHlkmm2VsLTFI6m2Um/LQaesiOFs61KYQ50ZiGA+6CNSTytYfORyY0MHQ6EC43W41tp8j5g+st8K4y+HtnGZGOXcZgeV7m+pG585Pxq/6s12380VNxIfEplaw2PLpL/DuLJUIsbEi4BOvpK+IEAnrrbTnyvaUs78K/Lry0egAmNqk7FKakdQzsB8j+9J0HsFhiKL1T/iNoP5VGX6kH3vOeYNWfGvceJqYVQPxZ7C23U69Z2bh+GFOmlMfdUL6kDU/Oa4Y/u25ubk1x/H3f/GXERN3EREQEREBERAREQEREBERAREQEREBERAREQEREDR/iHhivc1xoAe6dvw3IZG9AQ3+aQHDMZZ2G4ffzFstrEHcZT8950viOCSvSqUqgulRSjDY2YW0PI9D1nF3otRr1qDHM9M5S1vtADwuubYNcX5XDAX1lMsW/HnrpO1+A0nDEAKxvYqxzLoDcHbQk2023l3glDCKmXEKe8XMBVs1zfLY5V2a9zYC2/pMPA8UW4BIsPCCOY5DTzuOu/lJE4QhgyjQ2uCD7en/Mzs7deHxyx/xN1sDw9g1m0I5FibkEXB3J2/Zmn9p8DQJC4csLk3LXK28P2VNmJOtySNufOdGJdr2A6ActNyeuunztLdTh5tnfl/c66RbrwnHj77tv8ors9wkUXV2ctuRcWOm/rrbppfeZePxzZ6hsbfZAtobWPp1+kxcTix3ii4CkWsdb23sNztqR5++DxrFClTdjmYm62A1YkC1tLXzHl1jW2dsm9eE/8P8AhC1a1bEtcrTZaSC1gWUZmbqbZl9wZ0uQ/ZjhYw+Gp075msXdvxO5zMR5XNh0AEmJtJpxZZXKvYiJKpERAREQEREBERAREQEREBERAREQEREBERAREQPJyztdgGevWdFvUpsSF51UKKWQefMeYHUzqc0LiZIxdb+oH3yIJnyXUlb8GPytn055QxXjDAkBxmVjoRc3t5W09Ln1mwrxGsAEUgg787X5XI/TWUdp+AH/AL+HFvvug5EWOdQCL7arrfe198HA8bXw5trXIIsG1AB1BDAgXvf9BHWUa45XC6qVFQIQHcI76qrGxNgL5bnX2vLeI4rVKlGN1B9CR5X5X/2lyrxRBZ3KtlYdPAcupBPre5BkHxHjiurHTUWVVGZmOttwR53kTFrlzTSO/jCajXJFrvcj+W3Inmf78pIcPptXZqrXKIzFQT9qodHOvJR4R6tI7gnB6mJckXVASHe9+tlQ8zyvsL35WO9PhUSmERcqgWA/fpGVkjLjxuV26Lw181Gk3VEPzUGZUwOBn/8APQ/8af6RM+azw5LNWvYiJKCIiAiIgIiICIiAiIgIiICIiAiIgIiICIiAnkTHbFrsviPlt7mJLfAvMwAudANfSaDjK61K1R6bBlZtGGqmyqCQeYup1kx2vwNSthnGa+VqdQot7OiOrVF6tdQdOdrc5A8Lp5VA353HPUzHn61HX/8AJju2pKgmnnIrG9l6VUkjwMTc2F0J6lDpc9RY6Sbw62GsykX985jjbPDozxlnbUH7EOfv02HUh/8ASSfLnyldPsYqWNR81rDIi5EaxJAYi7EX5AgeU3VW0mNiNec0uVZY8c2iqOFRECoAABYKAAoHtMHFnfzvJWr0mBiafhP0Hpz/ACmVrqxxkbD2R4klSkKYPjpAKyncA3Ct6EKfcEcpPzgPH+I1aGIptQqPTqKrHMp3DNoGB0ceAnKQROn9gOPYnE4XvcQgJzsquoy94qhfGBsfEWXTmpnbhjbhMnlcupnZG4T2WqdUNsfbmPUS5Fij2IiAiIgIiICIiAiIgIiICIiAiIgeRKKlQDc2mI+Lvot/y/f0kyWotZdWqqi7EAecxziifsqT/M3hHtfUy0qa359efzOv1lTfWWmMiNoNMZVGNalWbwOoNJRotxqQTuWNj1+zyvNiCgCwkVxfhXeoLG1RDmRtrHQ2vyBsPQgHlHBOKd7enUGWsmjKdL20uo6dRyuNwQTlMrjlcb4vcdOeEz45yYzuTVn9pdZAYzhQRiyjwk3t+A8x/T06XmwkSqTnjMpqsuPO4Xca4E06dJcWZWLwRW7ILjmvMea9fT5dJgpUBH025jcEcj6zluFx8u7Hkmc3F64EtVVB9YD62vKc1/3b5ylrSTVY7jUSziV8BJIA1JJ2AHM9NJkalgoBLb5VFz6nko8zYSUpcIVgO9AI/Bup/r/F6besthhcv4Ryc2OE+3MOCdk3x+IbEVAyYUnwtqrV1GiinzCkC5bodNdV61SoLTVURQqKAiqosqqBYAAbACZRlIWd2+pPxHmZd22/lYZL8vfYj0Mj8fxjuHpIVL942XQ+JRcAEjYi56g+RsZlcU4ilBMzHXZV5seg/XlIjhuAdnOIrf8AcYWVeVJeluTWJ9LnmTKZZW2Y4+f6bcfHJLnyeO9fd+v4bKtZTpfXodD8jLkjip5fv2nq4h13AI9bGaXD0w2kJ7MSljFOhup6Np8jsZlSllnlL2IiAiIgIiICIiAiIgeTEr1zsvz/AElyuSdB7yhKcvJJ3UWscYa+5Nzz5y7So5ZkZYI2k3K1GlGSeKlzeXG6SoCV2aUGRPFuE94RUQ5Kq7MNL25N+vnzGkljErljMpqr4Z3C7iK4VxbOe7qjJVG6nQN5j9LnyuNZMgSKxWFoYgEZlZkNsysC1M7gEjbrYzFGMrYawrA1KewqgajpmHP96kzLdw6y8e29wx5O8Or6/wAbBIfjfBe+UlKj0atvDUXXbYOh8Lj11HIiSeHrq4DKQwOxEu3mvlh3jfVcZx/FeKUMQuGamtSo32CtMsKouBmUqQMo53Ay31tN44LwDFNlfF18p37iiAqjyaqQXO/3Suo3M2uwB21N9flf+0rizG+JE/qZ+Las0MOqCyqAPzPUnmfMy/EtVqyopZiABqSdAI8I7tVmRPFOMLS8K+OqdAg11O17bem/5zEq8RrYglcOpVNjVbT1sOR+v9O8zuG8ISiLjxOftOdSb726D9m8y+dz6w8e/wDG848ePvk8+v8AfTC4bwti3f1zmqfdX7tLoANrj5DzOsmrSswBNcMZjOmPJnc73/16k9RbyynJLpEqCy/yZ6YlSiDuJbouyaHVenMekzystVKf5SZlvqmtL6OCLjaVzBoHKbcj9JmylmqmXb2IiQkiIgIiICUk2lUtVDygUAS7llAErB+stUPJ6RpDCe8pApQTRviP2kqYT+HCqSrPnc3KZxTZD3WYbZrm/kNiLib2JSVkyyXdK0DB9qOJ4wD+FwK0FP8Aj4h2KeZVAqlvIi4k3hezBezY2u+KfmjeDDi/IUFsrDzbMZstotG/Qt0qSqAqqFUCwVQFAHkBtKnQEEEAg6EHUW6ESqJVLWqi/wAHVDLfuahsw5I3Ue2voD0E2TpMPi2G7yk68yLjyI1H1EsdncRnoLfdfD8tvpaY4/ty+P4vc/t0Z/v45nfMur9+qliIAnsTZzsHiOOWihdvQDmx5ASHw+AqYkipXJVN1pC405Fun5+m09xY77GLTP2aQzEdScp9/tL8jNhmOvnld+J+HTb+jjNebN79T8KadMKAFAAGgAFgB0AlU9ibOZSZUBAE9koU2nonsQEpYaysTy2sJWGSXaZ09NIaFOo8x+UW7iJNLkREhJERA//Z', 
            era: 2.78, kper9: 10.4, bbper9: 2.2 },
        }
    },
}
</script>

<style>
.stats-table {
  border-collapse: collapse;
  width: 95%;
  font-size: 12px;
  margin-bottom: 5px;
}

.stats-table th, .stats-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.stats-table th {
  background-color: #f2f2f2;
}
</style>